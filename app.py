from flask import Flask, render_template, request
# import json
from random import choice

app = Flask(__name__)

main_list = [
    {'country':'Polland','tour operator':'aviasales', 'count days': 10, 'price': 1000},
    {'country':'Turkey','tour operator':'aviasales', 'count days': 7, 'price': 5000},
    {'country':'Ukraine','tour operator':'alibabu', 'count days': 4, 'price': 3000},
    {'country':'Germany','tour operator':'aviasales', 'count days': 3, 'price': 2000},
    {'country':'USA','tour operator':'alibabu', 'count days': 4, 'price': 7000},
    {'country':'Sweden','tour operator':'aviasales', 'count days': 2, 'price': 4000},
    {'country':'Holland','tour operator':'aviasales', 'count days': 9, 'price': 3000},
    {'country':'Turkey','tour operator':'alibabu', 'count days': 8, 'price': 11000},
    {'country':'Argetina','tour operator':'aviasales', 'count days': 5, 'price': 1000},
    {'country':'Turkey','tour operator':'alibabu', 'count days': 6, 'price': 5320}
    
]

@app.route('/')
def index():
    countries = list(set([tour['country'] for tour in main_list]))
    return render_template('index.html', countries=countries)

@app.route('/process_form', methods=['POST'])
def process_form():
    selected_country = request.form.get('manufacturer')
    price_range = request.form.get('price_range')

    filtered_tours = [
        tour for tour in main_list
        if tour['country'] == selected_country
    ]

    if not selected_country or not price_range:
        return render_template('index.html', error="Все поля должны быть заполнены!", countries=list(set([tour['country'] for tour in main_list])))

    return render_template('results.html', tours=filtered_tours, country=selected_country, price_range=price_range)

@app.route('/tours/<operator>')
def first_task(operator):
    ready_tour = []
    for i in main_list:
        if i['tour operator'] == operator:
            ready_tour.append(i)
    print("checker", ready_tour)
    if ready_tour:       
        return render_template('tours.html', ready_tour=ready_tour, title="TOUR PAGE")
    else:
        return render_template('nosuch.html')
    
    # operator = None
    # return 'Hello world'


@app.route('/tours/days/<int:n>')
def second_task(n):
    count = int(n)
    count_days = []
    for day in main_list:
        if day['count days'] < count:
            count_days.append(day)
                 
    if count_days:
        return (render_template('days.html', count_days=count_days,title="Days Result"))
    else:
        return render_template('nosuch.html')


@app.route('/tours/turkey')
def third_task():
    result = []
    for tour in main_list:
        if tour['country'].lower() == 'turkey':
            result.append(tour)
    if result:
        expensive = None
        max_price = 0
        for tour in result:
            if tour['price']>max_price:
                expensive = tour
                max_price = tour['price']
        return render_template('expensive.html', tour=expensive, title="Самый дорогой тур в Турцию")
    else:
        return render_template('nosuch.html')


@app.errorhandler(404)
def error_page(error):
    return render_template('404.html', title="Error"),404

@app.route('/play', methods=['GET', 'POST'])
def play(): 
    if request.method == 'POST':
        player_choice = request.form.get('choice')
        options = ['rock', 'scissors', 'paper']
        computer_choice = choice(options)
        if player_choice == computer_choice:
            result = "Tie!"
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "scissors" and computer_choice == "paper") or \
             (player_choice == "paper" and computer_choice == "rock"):
            result = "You won!"
        else:
            result = "You lose!"

        return render_template('play.html', player_choice=player_choice, computer_choice=computer_choice, result=result)

    return render_template('play.html', player_choice=None, computer_choice=None, result=None)


if __name__ == ('__main__'):
    app.run(debug=True)
    