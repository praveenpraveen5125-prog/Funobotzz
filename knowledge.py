"""Central approved-knowledge database. Add organizer-supplied content here (topics/facts) without touching other code."""
SRC = "Funobotz Reference Pack 2/3 (store.funobotz.com, 2 Oct 2026)"
def C(name, emoji, intro, behaviour, topics, personality, status):
    return dict(name=name, emoji=emoji, intro=intro, behaviour=behaviour, topics=topics,
                personality=personality, source=SRC, status=status, image=None)  # image=None -> placeholder art
CHARACTERS = {
 "petalo": C("Petalo","🌸","A light-up discovery friend.","Light-up discovery friend used with challenge cards and connected subworlds.",["light","cause and effect","observation","safety awareness","communication"],"curious, gentle, sparkly","approved"),
 "quacky": C("Quacky","🦆","A movable duck bot.","Movable duck bot powered by a BO motor through a simple circuit.",["motor","battery","circuit","energy","cause and effect"],"cheerful, bouncy, loves to waddle","approved"),
 "tolly": C("Tolly","🚦","The timer-circuit friend.","Uses a timer circuit and a red-yellow-green LED sequence.",["timer","led","circuit","sequencing"],"calm, orderly, patient","approved"),
 "tiko": C("Tiko","🦂","A scorpio bot.","Scorpio bot whose motor creates up-and-down thread-based tail movement.",["motor","circuit","energy","troubleshooting"],"brave, tinkering, never gives up","approved"),
 "emoti": C("Emoti","😊","An expression bot.","Brings emotions to life through simple movements and reactions.",[],"expressive, warm","behaviour-only"),
 "mimo": C("Mimo","🐶","A paper pet dog.","Paper pet dog that comes to life through simple movement and playful interaction.",[],"playful, loyal","behaviour-only"),
 "kuttybot": C("Kuttybot","🤖","A friendly talking robot.","Friendly talking robot that speaks and interacts.",[],"chatty, friendly","behaviour-only"),
 "kutty_omni": C("Kutty Omni","⭐","Official Funobotz character.","",[],"friendly","pending-organizer-content"),
 "wavy": C("Wavy","🌊","Official Funobotz character.","",[],"friendly","pending-organizer-content"),
 "chicky": C("Chicky","🐥","Official Funobotz character.","",[],"friendly","pending-organizer-content"),
 "omni": C("Omni","🔷","Official Funobotz character.","",[],"friendly","pending-organizer-content"),
 "cuby": C("Cuby","🧊","Official Funobotz character.","",[],"friendly","pending-organizer-content"),
}
# concept -> (keywords, characters with approved mapping, interest group)
CONCEPTS = {
 "light": (["light","glow","colour","color","bright","lamp","dark"],["petalo"],"light"),
 "cause and effect": (["cause","effect","why does","what happens"],["petalo","quacky"],"light"),
 "motor": (["motor","move","moving","motion","robot","walk","spin","machine","tail","waddle"],["quacky","tiko"],"motors"),
 "battery": (["battery","batteries","power"],["quacky"],"electronics"),
 "energy": (["energy","electricity make","electric"],["quacky","tiko"],"motors"),
 "circuit": (["circuit","wire","current","electronic","connection"],["quacky","tolly","tiko"],"electronics"),
 "timer": (["timer","led","traffic","signal","sequence","red","green"],["tolly"],"electronics"),
 "troubleshooting": (["fix","broken","not working","stuck","troubleshoot"],["tiko"],"motors"),
}
FACTS = {  # level-graded explanations (general science + approved character context)
 "light": {"beginner":"Light helps us see! Petalo lights up so we can notice how light looks in different places. Try asking: what changes when it gets darker?","intermediate":"Light lets us observe the world. Petalo uses light to help us notice cause and effect: change something and watch what the light does.","advanced":"Light is a form of energy we detect with our eyes. With Petalo, we observe how lighting changes in environments and reason about cause and effect, while staying safe around bright lights."},
 "motor": {"beginner":"A motor makes things spin. Quacky the duck bot uses a BO motor, so a little motor helps it move!","intermediate":"Quacky's BO motor is joined to a battery with a simple circuit. When the circuit is complete, the motor turns and the duck moves. Tiko's motor pulls a thread to move its tail up and down.","advanced":"In Quacky, a battery supplies electrical energy through a simple circuit to a BO motor, which converts it to mechanical motion. Tiko applies the same energy-to-motion idea, using the motor to move a thread that lifts and lowers the tail."},
 "energy": {"beginner":"Batteries hold energy. The energy flows to the motor and makes Quacky move!","intermediate":"Electrical energy from the battery travels through the circuit and the motor turns it into movement.","advanced":"The battery's electrical energy is converted by the motor into mechanical energy (motion). Some energy is always lost as heat and sound."},
 "battery": {"beginner":"A battery is a tiny power box. It gives Quacky's motor the push to go!","intermediate":"A battery pushes electric current through a circuit. Quacky needs the battery connected correctly to move.","advanced":"A battery provides the potential difference that drives current through a closed loop; a break anywhere stops the motor."},
 "circuit": {"beginner":"A circuit is a path for electricity, like a track for a toy car. It must make a full loop!","intermediate":"A circuit connects a battery to parts like Quacky's motor or Tolly's LEDs. If the loop is broken, nothing works.","advanced":"A closed circuit lets current flow from the battery through components and back. Tolly's timer circuit controls when each LED turns on; check connections first when troubleshooting."},
 "timer": {"beginner":"Tolly's lights go red, yellow, green, one after another, like a traffic light!","intermediate":"Tolly uses a timer circuit to switch the red, yellow and green LEDs in order. That is electronic sequencing.","advanced":"A timer circuit controls timing, driving Tolly's red-yellow-green LED sequence. Sequencing like this appears in real-world electronics such as signals."},
 "cause and effect": {"beginner":"When you do something and something happens, that's cause and effect! Switch on, light glows.","intermediate":"Cause and effect: a change (cause) leads to a result (effect), like closing a circuit so Quacky moves.","advanced":"Predict, change one thing, observe the result: that's how Petalo's challenge cards build scientific thinking."},
 "troubleshooting": {"beginner":"If Tiko's tail won't move, check the little parts one at a time.","intermediate":"Troubleshooting means checking step by step: battery, connections, then the moving thread.","advanced":"Isolate the fault: power source, circuit connections, motor, then the mechanical linkage."},
}
INTEREST_OF = {"light":"light","cause and effect":"light","motor":"motors","energy":"motors","troubleshooting":"motors","battery":"electronics","circuit":"electronics","timer":"electronics"}
QUIZ = {
 "light":[("What does Petalo help us explore?",["Light","Cooking","Swimming"],0,"Petalo is a light-up discovery friend!")],
 "motor":[("What powers Quacky's movement?",["A BO motor","A balloon","A spring only"],0,"Quacky uses a BO motor through a simple circuit."),("What does Tiko's motor move?",["The tail with a thread","The wheels","A wing"],0,"Tiko's motor makes the thread-based tail go up and down.")],
 "circuit":[("A circuit must be...?",["A full loop","Broken","Wet"],0,"Electricity needs a complete path.")],
 "timer":[("What colours are in Tolly's LED sequence?",["Red, yellow, green","Blue, pink, white","Only red"],0,"Tolly's timer circuit runs red-yellow-green.")],
 "energy":[("A motor turns electrical energy into...?",["Motion","Water","Sound only"],0,"Electrical energy becomes mechanical motion.")],
}
