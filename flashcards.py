#!/usr/bin/env python3

import os
import json
import time
import datetime
import random
import argparse
import sys

# Hilfsfunktionen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_deck(deck_name, deck_data):
    with open(f"{deck_name}.json", 'w', encoding='utf-8') as f:
        json.dump(deck_data, f, ensure_ascii=False, indent=4)

def load_deck(deck_name):
    with open(f"{deck_name}.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def list_decks():
    return [f[:-5] for f in os.listdir() if f.endswith('.json')]

def get_timestamp():
    return int(time.time())

def get_human_readable_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_filter_time(offset, time_unit):
    now = datetime.datetime.now()
    if time_unit == 'h':
        return now - datetime.timedelta(hours=offset)
    elif time_unit == 'd':
        return now - datetime.timedelta(days=offset)
    elif time_unit == 'a':
        return now - datetime.timedelta(days=365*offset)

def add_card(deck_name):
    deck_data = load_deck(deck_name) if os.path.exists(f"{deck_name}.json") else []
    
    while True:
        clear_console()
        print("Neue Karte hinzufügen")
        vorderseite = input("Vorderseite: ").strip()
        if not vorderseite:
            print("Keine Vorderseite eingegeben, Abbruch.")
            break

        rueckseite = input("Rückseite: ").strip()
        if not rueckseite:
            print("Keine Rückseite eingegeben, Vorderseite verworfen.")
            continue

        timestamp = get_timestamp()
        human_time = get_human_readable_time()

        card = {
            "id": timestamp,
            "vorderseite": vorderseite,
            "rueckseite": rueckseite,
            "level": 1,
            "erstellt": human_time,
            "wiederholt": human_time
        }
        deck_data.append(card)
        save_deck(deck_name, deck_data)
        
        print(f"\nZuletzt hinzugefügt:\n{vorderseite} ({timestamp})\n")
        more = input("Weitere Karte hinzufügen? (j/n): ").lower()
        if more != 'j':
            break

def learn(deck_name, filters, sorters):
    deck_data = load_deck(deck_name)
    
    last_learned_card = None
    
    for filter_key, filter_value in filters.items():
        if filter_key.startswith('l') and filter_key[1].isdigit():
            if filter_key[1] == 'g':
                deck_data = [card for card in deck_data if card['level'] > int(filter_key[2])]
            elif filter_key[1] == 'k':
                deck_data = [card for card in deck_data if card['level'] < int(filter_key[2])]
            else:
                deck_data = [card for card in deck_data if card['level'] == int(filter_key[1])]
        elif filter_key.startswith('w') or filter_key.startswith('c'):
            filter_time = get_filter_time(int(filter_key[2:-1]), filter_key[-1])
            card_key = 'wiederholt' if filter_key.startswith('w') else 'erstellt'
            if filter_key.startswith('wk') or filter_key.startswith('ck'):
                deck_data = [card for card in deck_data if datetime.datetime.strptime(card[card_key], '%Y-%m-%d %H:%M:%S') >= filter_time]
            else:
                deck_data = [card for card in deck_data if datetime.datetime.strptime(card[card_key], '%Y-%m-%d %H:%M:%S') <= filter_time]
        elif filter_key == 'id':
            deck_data = [card for card in deck_data if card['id'] in filter_value]
    
    for sorter in sorters:
        if sorter == 'swauf':
            deck_data = sorted(deck_data, key=lambda x: x['wiederholt'])
        elif sorter == 'swab':
            deck_data = sorted(deck_data, key=lambda x: x['wiederholt'], reverse=True)
        elif sorter == 'scauf':
            deck_data = sorted(deck_data, key=lambda x: x['erstellt'])
        elif sorter == 'scab':
            deck_data = sorted(deck_data, key=lambda x: x['erstellt'], reverse=True)
        elif sorter == 'saauf':
            deck_data = sorted(deck_data, key=lambda x: x['vorderseite'])
        elif sorter == 'saab':
            deck_data = sorted(deck_data, key=lambda x: x['vorderseite'], reverse=True)
        elif sorter == 'r':
            random.shuffle(deck_data)

    for card in deck_data:
        clear_console()
        if last_learned_card:
            print(f"\nZuletzt gelernt:\n{last_learned_card['vorderseite']} ({last_learned_card['id']})\n")
        
        print(f"{card['vorderseite']}")
        input("")
        print(f"{card['rueckseite']}")
        
        answer = input("\nGewusst? (j/n/Level): ").lower()
        if answer == 'j':
            if card['level'] < 5:
                card['level'] += 1
        elif answer == 'n':
            if card['level'] > 1:
                card['level'] -= 1
        elif answer in ['1', '2', '3', '4', '5']:
            card['level'] = int(answer)
        
        card['wiederholt'] = get_human_readable_time()
        save_deck(deck_name, deck_data)
        
        last_learned_card = card


    if last_learned_card:
        print(f"\nZuletzt gelernt:\n{last_learned_card['vorderseite']} ({last_learned_card['id']})\n")
    print("Alle Karten im Deck durchgegangen!")




def list_cards(deck_name, filters, sorters, show_back):
    deck_data = load_deck(deck_name)

    for filter_key, filter_value in filters.items():
        if filter_key.startswith('l') and filter_key[1].isdigit():
            if filter_key[1] == 'g':
                deck_data = [card for card in deck_data if card['level'] > int(filter_key[2])]
            elif filter_key[1] == 'k':
                deck_data = [card for card in deck_data if card['level'] < int(filter_key[2])]
            else:
                deck_data = [card for card in deck_data if card['level'] == int(filter_key[1])]
        elif filter_key.startswith('w') or filter_key.startswith('c'):
            filter_time = get_filter_time(int(filter_key[2:-1]), filter_key[-1])
            card_key = 'wiederholt' if filter_key.startswith('w') else 'erstellt'
            if card_key in deck_data[0]:  # Überprüfen, ob der Schlüssel im ersten Karten-Dictionary existiert
                if filter_key.startswith('wk') or filter_key.startswith('ck'):
                    deck_data = [card for card in deck_data if datetime.datetime.strptime(card[card_key], '%Y-%m-%d %H:%M:%S') >= filter_time]
                else:
                    deck_data = [card for card in deck_data if datetime.datetime.strptime(card[card_key], '%Y-%m-%d %H:%M:%S') <= filter_time]
        elif filter_key == 'id':
            deck_data = [card for card in deck_data if card['id'] in filter_value]

    for sorter in sorters:
        if sorter == 'swauf':
            deck_data = sorted(deck_data, key=lambda x: x['wiederholt'])
        elif sorter == 'swab':
            deck_data = sorted(deck_data, key=lambda x: x['wiederholt'], reverse=True)
        elif sorter == 'scauf':
            deck_data = sorted(deck_data, key=lambda x: x['erstellt'])
        elif sorter == 'scab':
            deck_data = sorted(deck_data, key=lambda x: x['erstellt'], reverse=True)
        elif sorter == 'saauf':
            deck_data = sorted(deck_data, key=lambda x: x['vorderseite'])
        elif sorter == 'saab':
            deck_data = sorted(deck_data, key=lambda x: x['vorderseite'], reverse=True)
        elif sorter == 'r':
            random.shuffle(deck_data)

    clear_console()
    for card in deck_data:
        print(f"{card['vorderseite']}")
        if show_back:
            print(f"  {card['rueckseite']}")
        print("")



# Hauptprogramm
def main():
    parser = argparse.ArgumentParser(description="Karteikarten-Anwendung")
    parser.add_argument("--add", nargs='?', const=True, help="Karte hinzufügen")
    parser.add_argument("--learn", nargs='?', const=True, help="Lernen starten")
    parser.add_argument("--list", nargs='?', const=True, help="Karten anzeigen")
    parser.add_argument("--back", action='store_true', help="Rückseite anzeigen")
    
    # Filter- und Sortieroptionen
    parser.add_argument("-l1", action='store_true', help="Level 1 Karten")
    parser.add_argument("-lg1", action='store_true', help="Level größer 1 Karten")
    parser.add_argument("-lk1", action='store_true', help="Level kleiner 1 Karten")
    parser.add_argument("-l2", action='store_true', help="Level 2 Karten")
    parser.add_argument("-lg2", action='store_true', help="Level größer 2 Karten")
    parser.add_argument("-lk2", action='store_true', help="Level kleiner 2 Karten")
    parser.add_argument("-l3", action='store_true', help="Level 3 Karten")
    parser.add_argument("-lg3", action='store_true', help="Level größer 3 Karten")
    parser.add_argument("-lk3", action='store_true', help="Level kleiner 3 Karten")
    parser.add_argument("-l4", action='store_true', help="Level 4 Karten")
    parser.add_argument("-lg4", action='store_true', help="Level größer 4 Karten")
    parser.add_argument("-lk4", action='store_true', help="Level kleiner 4 Karten")
    parser.add_argument("-l5", action='store_true', help="Level 5 Karten")
    parser.add_argument("-lk5", action='store_true', help="Level kleiner 5 Karten")
    
    parser.add_argument("-wk1h", action='store_true', help="Wiederholt in letzter Stunde")
    parser.add_argument("-wk24h", action='store_true', help="Wiederholt in letzten 24 Stunden")
    parser.add_argument("-wk7d", action='store_true', help="Wiederholt in letzter Woche")
    parser.add_argument("-wk30d", action='store_true', help="Wiederholt in letztem Monat")
    parser.add_argument("-wk1a", action='store_true', help="Wiederholt in letztem Jahr")
    parser.add_argument("-wg1h", action='store_true', help="Wiederholt vor mehr als 1 Stunde")
    parser.add_argument("-wg24h", action='store_true', help="Wiederholt vor mehr als 24 Stunden")
    parser.add_argument("-wg7d", action='store_true', help="Wiederholt vor mehr als 1 Woche")
    parser.add_argument("-wg30d", action='store_true', help="Wiederholt vor mehr als 1 Monat")
    parser.add_argument("-wg1a", action='store_true', help="Wiederholt vor mehr als 1 Jahr")
    
    parser.add_argument("-ck1h", action='store_true', help="Erstellt in letzter Stunde")
    parser.add_argument("-ck24h", action='store_true', help="Erstellt in letzten 24 Stunden")
    parser.add_argument("-ck7d", action='store_true', help="Erstellt in letzter Woche")
    parser.add_argument("-ck30d", action='store_true', help="Erstellt in letztem Monat")
    parser.add_argument("-ck1a", action='store_true', help="Erstellt in letztem Jahr")
    parser.add_argument("-cg1h", action='store_true', help="Erstellt vor mehr als 1 Stunde")
    parser.add_argument("-cg24h", action='store_true', help="Erstellt vor mehr als 24 Stunden")
    parser.add_argument("-cg7d", action='store_true', help="Erstellt vor mehr als 1 Woche")
    parser.add_argument("-cg30d", action='store_true', help="Erstellt vor mehr als 1 Monat")
    parser.add_argument("-cg1a", action='store_true', help="Erstellt vor mehr als 1 Jahr")
    
    parser.add_argument("-id", nargs='+', type=int, help="Filter nach IDs")
    
    parser.add_argument("-swauf", action='store_true', help="Sortiere nach 'wiederholt' aufsteigend")
    parser.add_argument("-swab", action='store_true', help="Sortiere nach 'wiederholt' absteigend")
    parser.add_argument("-scauf", action='store_true', help="Sortiere nach 'erstellt' aufsteigend")
    parser.add_argument("-scab", action='store_true', help="Sortiere nach 'erstellt' absteigend")
    parser.add_argument("-saauf", action='store_true', help="Sortiere nach Vorderseite aufsteigend")
    parser.add_argument("-saab", action='store_true', help="Sortiere nach Vorderseite absteigend")
    parser.add_argument("-r", action='store_true', help="Zufällige Sortierung")
    
    args = parser.parse_args()

    filters = {k: v for k, v in vars(args).items() if v and k.startswith(('l', 'wk', 'wg', 'ck', 'cg', 'id'))}
    sorters = [k for k, v in vars(args).items() if v and k.startswith(('sw', 'sc', 'sa', 'r'))]

    if args.add is not None:
        deck_name = args.add if args.add is not True else None
        if not deck_name:
            decks = list_decks()
            if decks:
                print("Wählen Sie ein Deck:")
                for i, deck in enumerate(decks, 1):
                    print(f"{i}. {deck}")
                print(f"{len(decks) + 1}. Neues Deck")
                
                choice = input("Ihre Wahl: ")
                if choice.isdigit() and 1 <= int(choice) <= len(decks):
                    deck_name = decks[int(choice) - 1]
                else:
                    deck_name = input("Neuen Decknamen eingeben: ").strip()
            else:
                deck_name = input("Neuen Decknamen eingeben: ").strip()
        if deck_name:
            add_card(deck_name)
    
    elif args.learn is not None:
        deck_name = args.learn if args.learn is not True else None
        if not deck_name:
            decks = list_decks()
            if len(decks) == 1:
                deck_name = decks[0]
            elif len(decks) > 1:
                print("Wählen Sie ein Deck:")
                for i, deck in enumerate(decks, 1):
                    print(f"{i}. {deck}")
                choice = input("Ihre Wahl: ")
                if choice.isdigit() and 1 <= int(choice) <= len(decks):
                    deck_name = decks[int(choice) - 1]
            else:
                print("Keine Decks gefunden.")
                sys.exit()
        if deck_name:
            learn(deck_name, filters, sorters)
    
    elif args.list is not None:
        deck_name = args.list if args.list is not True else None
        if not deck_name:
            decks = list_decks()
            if len(decks) == 1:
                deck_name = decks[0]
            elif len(decks) > 1:
                print("Wählen Sie ein Deck:")
                for i, deck in enumerate(decks, 1):
                    print(f"{i}. {deck}")
                choice = input("Ihre Wahl: ")
                if choice.isdigit() and 1 <= int(choice) <= len(decks):
                    deck_name = decks[int(choice) - 1]
            else:
                print("Keine Decks gefunden.")
                sys.exit()
        if deck_name:
            list_cards(deck_name, filters, sorters, args.back)
    
    else:
        decks = list_decks()
        if len(decks) == 1:
            learn(decks[0], filters, sorters)
        elif len(decks) > 1:
            print("Wählen Sie ein Deck:")
            for i, deck in enumerate(decks, 1):
                print(f"{i}. {deck}")
            choice = input("Ihre Wahl: ")
            if choice.isdigit() and 1 <= int(choice) <= len(decks):
                learn(decks[int(choice) - 1], filters, sorters)
        else:
            print("Keine Decks gefunden.")
            sys.exit()

if __name__ == "__main__":
    main()

