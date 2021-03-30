from .package1.sample3 import %G, $y

$x = 5

%H @body y=5:
    | {x+y}
    @body
    | {x*y}

$x = 155
$z = 155 + y
