# Comp469-Robobrain
This repository contains robot code for our Fall 2017 Artificial Intelligence class. 

In this class, we worked on a variety of different AI algorithms while also devolping a basic autonomous robot to be guided using those algorithms. The penultimate task was driving the robot using a Q-Learning Pacman simulation. Two versions of that simulation are included here: a standalone version under pacbrain_bot, and a version that relies on a communicating Arduino - under the week15 folder.

## Pacman
Our simulation is a very basic one, but the process goes like this:
1. Pacman decides the best course of action.
2. Pacman takes that action.
3. The two ghosts take their actions.
4. Pacman gets the resulting reward - did he win? Did he die? Or something else, perhaps?
5. Pacman uses the reward and the Q values to update the feature weights.
6. Repeat until victory or death!

That consitutes one "game" of Pacman. In the demo, we play 30 games in order to get a decent sample of Q-Learning.

## Notes on Q-Learning
Also, for lack of a better place to document all this, here are some notes and observations about Q-Learning.

Equal attention should be given to both the features and the "rewards" or "utility" of each state. For our simulation, it was guaranteed every turn that Pacman would move and the ghosts would move. Thus, we had four outcomes:
* Pacman eats nothing. Reward: -1
* Pacman eats a dot. Reward: 1
* Pacman gets eaten by a ghost. Reward: -15
* Pacman eats the last dot. Reward: 10
 
Now, for our features, we essentially tested three elements for each action:
* Will this action make Pacman eat a dot?
* Will this action make Pacman get eaten by a ghost?
* How many times has Pacman visited this cell?

You can see how our enumeration of outcomes has an effect on what we test using our features - view "feature.py" to see our feature functions. Each feature vector returns different values dependent on the state of those four things.

Generally, we tried to design the feature functions so that they only tested one of these elements. 

Our features could ultimately be summed up like so:
1. If Pacman ran into a ghost, return 1. Otherwise, return 0.
2. If Pacman ate a dot, return 1. Otherwise, return 0.
3. Return the amount of times Pacman has visited this cell, divided by the global maximum of cell visits.

That last function is essentially an exploration function - it forces Pacman to prioritize areas he hasn't gone to before. In Pacman, that also means areas that will have dots in them!

Avoid features that returns negatives. Early on we were doing this to indicate a feature was undesirable. It worked poorly. Instead, you should try to return a positive value and have the reward of the state naturally turn the feature weight negative over time. So, rather than having a collision with a ghost rated as -1, we return 1 and Pacman learns that ghosts are bad *the hard way*.

### Q-Learning: Lessons Learned 
* Try and normalize your feature functions so they return values between 0 and 1.
* Boolean or binary features (features that return either 0 or 1) work really well.
* Don't make negative features, make negative rewards.
* Feature functions that only test one feature work best!
* It is best to make failure more punishing than winning is rewarding. This prevents the AI from completely forgetting lessons learned from failure. If the AI isn't failing, it's succeeding! 