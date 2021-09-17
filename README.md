# Booking for UCD Gym

Automated booking for UCD gym so you don't miss out on the time slot you want.

Since reopening of gyms in Ireland (after closure for the Covid19 pandemic) my university gym requires booking the gym.  
Booking for each timeslot opens 3 hours before the respective timeslot.
This became a problem for me when undergraduates returned and the slots booked out almost instantly (even at 6 in the morning).
This program is written to prevent me having to get up at 6am and refreshing my browser just to get a gym slot 3 hours later.

---

## To Do

- convert to c++ program
- speed up python implementation
- more options for timeslots
- GUI

---

## Contents

[Gym Booking](#gym-booking)

- [1. Environment](#1-environment)
- [2. Booking](#2-booking)

---

## 1. Environment

Creating a virtual environment to install the dependencies packages is recommended, this can be done with either conda or the python3 venv.

### Using [`conda`](https://docs.conda.io/en/latest/)

```bash
conda env create -f environment.yml
conda activate gymbooking
```

### Allow execution of script

To run the script you must first make it executable by using chmod

```bash
sudo chmod a+x book.sh
```

#### exporting dependencies to yml file

```bash
conda env export > environment.yml
```

## 2. Booking

To run the script after downloading the repo from github you simply configure the [`config.json`](config.json) file with your own student number and preferred time slot. Then in the terminal before you want to shutdown your computer you run the script with.

```bash
source ./book.sh
```
