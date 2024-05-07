"""Finite-state machine"""

import random
import time


class FSM:
    """Finite-state machine"""

    EAT = {
        "breakfast": {
            "pizza slice": 12,
            "pancakes": 10,
            "eggs": 8,
            "cereal": 6,
            "toast": 4,
        },
        "snack": {"apple": 4, "banana": 3, "orange": 2, "grapes": 2, "strawberries": 2},
        "lunch": {"soup": 8, "salad": 5, "sandwich": 3, "burger": 6, "pizza": 10},
        "dinner": {"steak": 15, "pasta": 13, "fish": 10, "chicken": 9, "rice": 8},
    }

    STUDY = ("Discrete Mathematics", "Calculus", "Fundamentals of Programming")

    REST = {
        "albums": {
            "Have A Nice Life - Deathconsciousness": -5,
            "The Microphones - The Glow Pt. 2": 5,
            "Slowdive - Souvlaki": 3,
            "Daft Punk - Random Access Memories": 4,
            "Radiohead - In Rainbows": -1,
            "Taylor Swift - 1989": -5,
        },
        "games": {
            "The Witcher 3: Wild Hunt": -2,
            "The Elder Scrolls V: Skyrim": 5,
            "Dark Souls III": -3,
            "Sekiro: Shadows Die Twice": 2,
            "Demon's Souls": 2,
            "Dota 2": -5,
        },
        "movies": {
            "Drive": -2,
            "La La Land": 4,
            "Oldboy": -4,
            "Taxi Driver": 3,
            "Pulp Fiction": 5,
        },
    }

    def __init__(self):
        self._hunger = 20
        self._energy = 20
        self._mood = 20
        self.current_state = None
        self.state_sleep = self._sleep()
        self.state_eat = self._eat()
        self.state_study = self._study()
        self.state_rest = self._rest()
        self.state_death = self._death()
        self.state_exam = self._exam()

    def send_hour(self, hour):
        """Send the hour to the current state"""
        if self._is_dead:
            self.current_state = self.state_death
        self.current_state.send(hour)

    @property
    def _is_dead(self):
        return not all([self.hunger, self.energy, self.mood])

    @property
    def current_state_name(self):
        """Return the name of the current state"""
        match self.current_state:
            case self.state_sleep:
                return "Sleep"
            case self.state_eat:
                return "Eat"
            case self.state_study:
                return "Study"
            case self.state_rest:
                return "Rest"
            case self.state_death:
                return "Death"
            case _:
                return None

    @property
    def hunger(self):
        """Return the hunger value"""
        return self._hunger

    @hunger.setter
    def hunger(self, value):
        self._hunger = min(max(0, value), 20)

    @property
    def energy(self):
        """Return the energy value"""
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = min(max(0, value), 20)

    @property
    def mood(self):
        """Return the mood value"""
        return self._mood

    @mood.setter
    def mood(self, value):
        self._mood = min(max(0, value), 20)

    @staticmethod
    def time_generator():
        """Time generator"""
        hour = 0
        while True:
            yield hour
            hour += 1
            hour %= 24

    @staticmethod
    def time_to_str(hour):
        """Convert the hour to a string"""
        if hour == 0:
            return " 12 AM "
        if hour < 12:
            if hour in (10, 11):
                return f"{hour} AM "
            return f"  {hour} AM "
        if hour == 12:
            return " 12 PM "
        if hour - 12 in (10, 11):
            return f" {hour-12} PM "
        return f"  {hour-12} PM "

    def _sleep(self):
        while True:
            hour = yield
            random_number = random.randint(1, 20)

            print("You are sleeping... 💤")
            self.energy += 2
            self.hunger -= 1

            if hour == 7 and random_number > 3:
                print("You woke up! What a beautiful day!")
                self.mood = random.randint(15, 20)
                self.current_state = self.state_eat
            elif hour == 7 and random_number > 1:
                print("You woke up in a bad mood :(")
                self.mood = random.randint(10, 14)
                self.current_state = self.state_eat
            elif hour == 8:
                print("You overslept and missed the breakfast!")
                self.mood = random.randint(5, 12)
                self.current_state = self.state_study

    def _eat(self):
        while True:
            hour = yield
            if random.randint(1, 50) == 1:  # 2%
                print(
                    "You forgot to buy food, so you were left with an empty fridge. 😵"
                )
                self.hunger -= 1
                self.mood -= 2
            elif self.mood <= 5 and random.randint(1, 5) == 5:
                print("You are not in the mood to eat anything. 😞")
                self.hunger -= 1
            else:
                self.mood += 2
                match hour:
                    case 8:
                        food = random.choice(list(FSM.EAT["breakfast"].keys()))
                        print(
                            f"Breakfast time! For breakfast, you chose {food}. Yummy! 🥞"
                        )
                        self.hunger += FSM.EAT["breakfast"][food]
                    case 11:
                        food = random.choice(list(FSM.EAT["snack"].keys()))
                        print(f"Snack time! For snack, you chose {food}. Yummy! 🍎")
                        self.hunger += FSM.EAT["snack"][food]
                    case 15:
                        food = random.choice(list(FSM.EAT["lunch"].keys()))
                        print(f"Lunch time! For lunch, you chose {food}. Yummy! 🍛")
                        self.hunger += FSM.EAT["lunch"][food]
                    case 21:
                        food = random.choice(list(FSM.EAT["dinner"].keys()))
                        print(f"Dinner time! For dinner, you chose {food}. Yummy! 🍖")
                        self.hunger += FSM.EAT["dinner"][food]

            if hour == 8:
                self.current_state = (
                    self.state_exam if random.randint(1, 5) == 5 else self.state_study
                )
            elif hour == 11:
                self.current_state = self.state_rest
            else:  # 15 or 21
                self.current_state = random.choice([self.state_study, self.state_rest])

    def _study(self):
        while True:
            hour = yield
            course = random.choice(FSM.STUDY)
            lecture_difficulty = random.randint(1, 3)
            understood = random.choice([True, False])
            self.hunger -= 1

            if hour in (9, 10, 11):
                print(f"You have come to a lecture on {course}. 📚")
                if understood:
                    print("You understood everything! 🤓")
                    self.mood += 2
                    self.energy -= 1
                else:
                    print(
                        "Lecture was really hard and you didn't understand anything. 😞"
                    )
                    self.mood -= lecture_difficulty
                    self.energy -= lecture_difficulty
            else:
                print(f"You are studying {course}. 📚")
                self.energy -= 1

            if hour == 9:
                if random.randint(1, 5) == 5:
                    self.current_state = self.state_exam
            elif hour == 10:
                if self.hunger <= 10:
                    self.current_state = self.state_eat
            elif hour == 11:
                print("Time to rest!")
                self.current_state = self.state_rest
            elif hour == 13:
                pass
            elif hour in (14, 20):
                self.current_state = self.state_eat
            else:
                if hour == 1 or (hour in (23, 0) and random.randint(1, 5) != 5):
                    self.current_state = self.state_sleep
                elif random.randint(1, 3) == 1:
                    print("Time to rest!")
                    self.current_state = self.state_rest

    def _exam(self):
        while True:
            hour = yield
            course = random.choice(FSM.STUDY)
            print(f"You have an exam in {course} today! 📝")
            self.energy -= 3
            self.hunger -= 2
            if random.randint(0, 1):
                print("You failed the exam! 😭")
                self.mood -= 5
            else:
                print("You passed the exam! 🎉")
                self.mood += 5

            if hour == 9:
                if random.randint(1, 5) != 5:
                    self.current_state = self.state_study
            else:
                if self.hunger <= 10:
                    self.current_state = self.state_eat
                else:
                    self.current_state = self.state_study

    def _rest(self):
        while True:
            hour = yield
            random_number = random.randint(1, 3)
            self.energy += 1
            self.hunger -= 1
            if random_number == 1:
                print("You decided to listen to music and relax. 🎧")
                album = random.choice(list(FSM.REST["albums"].keys()))
                self.mood += FSM.REST["albums"][album]
                print(f"You chose to listen to {album}.", end=" ")
                if FSM.REST["albums"][album] > 0:
                    print("You feel better! 😊")
                else:
                    print("You feel worse! 😞")
            elif random_number == 2:
                print("You decided to play a game. 🎮")
                game = random.choice(list(FSM.REST["games"].keys()))
                self.mood += FSM.REST["games"][game]
                print(f"You chose to play {game}.", end=" ")
                if FSM.REST["games"][game] > 0:
                    print("You feel better! 😊")
                else:
                    print("You feel worse! 😞")
            elif random_number == 3:
                print("You decided to watch a movie. 🎬")
                movie = random.choice(list(FSM.REST["movies"].keys()))
                self.mood += FSM.REST["movies"][movie]
                print(f"You chose to watch {movie}.", end=" ")
                if FSM.REST["movies"][movie] > 0:
                    print("You feel better! 😊")
                else:
                    print("You feel worse! 😞")

            if hour == 12:
                print("Time to study!")
                self.current_state = self.state_study
            elif hour == 20:
                self.current_state = self.state_eat
            else:
                if hour == 1 or (hour in (23, 0) and random.randint(1, 5) != 5):
                    self.current_state = self.state_sleep
                elif random.randint(1, 3) == 1:
                    print("Time to study!")
                    self.current_state = self.state_study

    def _death(self):
        while True:
            _ = yield
            if self.hunger == 0:
                print("You died of hunger!")
            elif self.energy == 0:
                print("You died of exhaustion!")
            elif self.mood == 0:
                print("You died of sadness!")

    def start_generators(self):
        """Start the generators"""
        next(self.state_sleep)
        next(self.state_eat)
        next(self.state_study)
        next(self.state_rest)
        next(self.state_death)
        next(self.state_exam)

    def run(self, verbosity=False, sleep_time=0.5):
        """Run the finite-state machine

        verbosity: bool, optional
            If True, print the current state and the values of hunger, energy, and mood
            Default is False
        sleep_time: float, optional
            Time to sleep between states
            Default is 0.5
        """
        states = 0
        self.start_generators()
        self.current_state = self.state_sleep
        time_generator = self.time_generator()
        while True:
            current_time = next(time_generator)
            print("\n" + "-" * 25 + self.time_to_str(current_time) + "-" * 25)
            if verbosity:
                print(
                    f"(Current state: {self.current_state_name}, \
Hunger: {self.hunger}, Energy: {self.energy}, Mood: {self.mood})"
                )
            self.send_hour(current_time)
            states += 1
            if self.current_state == self.state_death:
                print(
                    f"Total days survived: {states//24} days, \
{states%24} hours. 💀 ({states} states)"
                )
                break
            if sleep_time:
                time.sleep(sleep_time)


if __name__ == "__main__":
    fsm = FSM()
    fsm.run(True, 0)  # verbosity, sleep_time
