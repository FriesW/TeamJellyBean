width_in = 2.79;
height_in = 2.08;
edge_margin_in = 0.15;

bottom_margin = .1;


margin = -3;
cup_depth = 4;
cup_width = 17 + 7;
cup_height = 11 + 7;
cup_lift = .3; //[-1, 1]

RESOLUTION = 50;

row_toggle = false;


in_to_mm = 25.4;

main_edge = edge_margin_in * in_to_mm;
main_w = width_in * in_to_mm;
main_h = height_in * in_to_mm;
main_d = cup_depth + bottom_margin;

difference(){
    //translate([- main_w / 2, - main_h / 2, - main_d])
    translate([0, 0, - main_d])
    cube([main_w, main_h, main_d]);
    
    /*union(){
        line(true);
        translate([0,2,0]) line(false);
    }*/
    translate([main_edge, main_edge, 0])
    grid(main_w - main_edge*2, main_h - main_edge*2);
    
}


module grid(length, width){
    center_distance = cup_height + margin;
    cutoff = width / center_distance - 1;
    for(x = [0:cutoff])
    {
        translate([0,x*center_distance,0])
        line(length, x%2==0 == row_toggle);
    }
}

module line(length, oddity=true){
    center_distance = cup_width + margin;
    c_offset = oddity ? center_distance : center_distance / 2;
    cutoff = oddity ? length - center_distance * 2 : length - center_distance; //could be better
    
    translate([c_offset, cup_height/2 + margin/2, 0])
    for(x = [0:center_distance:cutoff])
        translate([x,0,0])
        dimple();
}

module dimple(){
    resize([cup_width, cup_height, cup_depth])
    intersection(){
        translate([0,0, cup_lift])
        sphere($fn=RESOLUTION);
        translate([-1, -1, -1 + cup_lift])
        cube([2, 2, 1 - cup_lift + 0.01]); //0.01 for clean face cutting
    }
}