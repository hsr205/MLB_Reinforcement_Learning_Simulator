
(*You might say "hodge, these are contsants, they should be all caps"*)
(*My response to that is, OCaml does not do constants, all variables are immutable by default*)
(*If you reassign a variable, it is actually just a copy of a variable within scope*)
(*Crazy right? and we are just getting started*)
(*Weight in grams*)
let ball_mass: int = 145
(*Radius in CM*)
let ball_radius: float = 3.48
(*Gravity m/s^2 *)
let gravity: float = 9.80665



(*ahhhh i love syntax*)
let print_the_specs() = 
    Printf.printf "The mass of a baseball is %d grams\n" ball_mass;
    Printf.printf "The radius of a baseball is %f ball_radius\n" ball_radius;
    Printf.printf "Gravity is %f m/s^2 \n" gravity;