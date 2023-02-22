from unittest.mock import Mock

MS = Mock()

# sceario 1 - fly loop

# navigation checks position, course and distance:
target_planet_name = "Earth"
target_position = MS.navigation_data.check("Earth")
# 1235, 456

MS.current_position
# 567, 43

target_angle = get_angle(from=MS.current_position, to=target_position)
# 34.4

target_distance = get_distance(MS.current_position, target_position)
# 3456

# engineering checks ship max speed
MS.engine.max_velocity
# 150 per second
# so, with 100% power, it will take 3456/150=23.04 seconds to get there.

# pilot set target_angle
MS.control.target_angle = target_angle
MS.rotation_thrusters.power_percent = 100
p # pilot receives update when ship rotates to target_angle
MS.rotation_thrusters.power_percent = 0

# pilot sets power to get wanted speed
MS.thrusters.power_percent = 100
MS.thrusters.cut_off_time = 20 # turn off engine after 20 seconds

# we are flying!


# okej, jak będziemy o tym myśleć per panel, to jest trochę łatwiej - ustalamy, jakie atrybut i funkcje ma każdy z modułów.
# ale jedźmy dalej, miałem tu parę sytuacji jeszcze do przetestowania
# może idźmy dalej, w końcu trzeba gdzieś wylądować:

# navigation checks distance again:
get_distance(MS.current_position, target_position)
# 17
# navigation checks course again - btw we can consider checking course by the pilot, navigation would only check coords

target_angle = get_angle(from=MS.current_position, to=target_position)
MS.control.target_angle = target_angle
p
# pilot waits for rotation # TODO: rotation seems like a great candidate for continuous operations procedure
# we still have 150 per second - and we need to travel 17 units.

# hm. This is getting complicated. I think we should add autopilot feature go_to_target(target_position) which would
# fly there and stop the engines. It would work on max 10% of engine.
# yep, it makes sense.

MS.control.go_to_target(target_position)
# control: ... autopilot set for 1235, 456. ETA: T+1 second
p
# control: Target destination reached. Switched to manual control.

# przy okazji, wyklarowała się nowa rzecz: w logu będziemy wyświetlać nazwę modułu, z którego log pochodzi.

# now we need to leave HyperSpace. Assuming it's a habitated space, we need to:
# ask for permission to enter normal space
# make sure we won't collide with anything. Collision check is valid for 10 seconds.

# actually, flight control can give us best place to disengage, which should be free for 30 seconds.

# Comms:
receivers = MS.transmitter.get_signals() # signals? receivers? I mean devices capable of receiving transmission
print(receivers)
[Docking Station Flight Control, Ship 1, Ship 2, Ship 3, Ship 4]
station = receivers[0]
# hmm. Now we need to prepare transmission. Transmission will be an object with the proper Metadata.
# I thought to make it easier, I will give interface with possible

transmission = station.new_transmission()
transmission.request_space_entry_permission()
transmission.send()
# transmission sent
p
#
#
# new transmission received: Permission granted.
last_transmission = MS.receiver.transmissions[-1]
print(last_transmission.text)
# "Greetings Mothership Cyklon,
#
# This is Jordan's Dock. We have received your request and we grant permission for you to enter normal space. Please proceed with caution and follow the suggested coordinates for safe entry: x = -98.57, y = 45.32.
#
# We advise you to closely monitor your ship's systems and ensure that all safety protocols are in place. Our station is monitoring your approach and will assist if necessary.
#
# Safe travels,
# Jordan's Dock."

# Also, the station might list commodities or panels which are forbidden here and ask the crew if they have them. The crew might lie.
# Station might later check that, or might not.

# we can also check:
transmission.details["safe_coordinates"]
#(-98.57, 45.32)


# hm. I think pilot should only have access to controller, not the engine or thrusters. Engineer should have access to
# engine or thruster. So panels cooperate with each other - controller sets something on the engine. Controller might work properly, but engine might not -
# engine might give wrong data.

# PILOT:
MS.control.normal_space_coords = (-98.57, 45.32)
# moving between hyperspace and normal space is risky - some panels should be turned off or they might get damaged,
# so the pilot or captain should ask to prepare for disengagement.

# e.g. Engineer may want to turn off shields or thrusters or something
MS.engine.running=False
# Engine turned OFF.
# Comms might want to turn off receiver:
MS.receiver.running = False

# panels should have attribute: Hyperspace transition safety, which shows percentage of some kind of failure if the device
# is active during hyperspace transition.
# crew can run panel.condition to display a dict with all data about the panel, including hyperspace_transition_safety.

# CAPTAIN: Is crew ready to enter normal space?
# CREW: ready.
# Captain: Punch it.
# PILOT:
MS.control.disengage_hyperdrive()
# entering normal space in x seconds...
# 3
# 2
# 1
# Entered normal space.

# włączamy to co powyłączaliśmy
MS.receiver.running = True
MS.engine.running = True

# Ok, teraz trzeba zadokować na stacji.
transmission = station.new_transmission()
transmission.request_docking_permission()
transmission.send()
P
# Receiver: Transmission received

last_transmission = MS.receiver.transmissions[-1]
print(last_transmission.text)
# "Greetings Spacecraft Vanguard,
#
# This is Station Omega. Your docking request has been received and approved. Please proceed with caution as you approach the station.
#
# We advise you to follow all standard docking procedures and verify that your ship's systems are functioning properly. Our station staff is ready to assist if needed.
#
# Welcome to Station Omega,
# Safe travels."

# Pilot should allign with the docking port.

MS.control.align_with_station()
# this can take a moment
# pilot is being updated
# ship aligned properly

# engineer has to lock docking clams when the ship is aligned.
MS.docking_clams.lock()




