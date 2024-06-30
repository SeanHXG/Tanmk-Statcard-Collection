import 'bootstrap/dist/css/bootstrap.css';
import TableBody from "./TableBody";
import TableHead from "./TableHead";
import { useState } from "react";

function PartTable({filters, data}) {

    const [tableData, setTableData] = useState(data);
    let Columns = []

    switch(filters.type){
        case 'hulls':
            Columns = [
                {category: 'Name', key: 'name'},
                {category: 'Tier', key: 'tier'},
                {category: 'Rarity', key: 'rarity'},
                {category: 'Weight', key: 'weight'},
                {category: 'Accel.', key: 'acceleration'},
                {category: 'Front Armor', key: 'armor_front'},
                {category: 'Side Armor', key: 'armor_side'},
                {category: 'Rear Armor', key: 'armor_rear'},
                {category: 'Speed Forwards', key: 'max_forwards'},
                {category: 'Speed Backwards', key: 'max_backwards'},
                {category: 'Torque', key: 'torque'},
                {category: 'Wheeled', key: 'wheeled'},
                {category: 'Traverse Rate', key: 'traverse_rate'},
                {category: 'Turning Radius', key: 'turning_radius'},
                {category: 'Ammo Storage', key: 'ammo_storage'},
                {category: 'Blowout', key: 'blowout'},
                {category: 'Hull Aim', key: 'hull_aim'},
                {category: 'Turretless', key: 'turretless'},
                {category: 'Crew Count', key: 'crew'},
                {category: 'Obtain', key: 'obtain'},
                {category: 'Price', key: 'price'},
            ]
            break;
        case 'turretless':
            Columns = [
                {category: 'Reload Multi', key: 'reload_multi'},
                {category: 'Clip', key: 'clip'},
                {category: '↔️ Limits', key: 'h_limits'},
                {category: '↕️ Limits', key: 'v_limits'},
                {category: 'Min Zoom', key: 'min_zoom'},
                {category: 'Max Zoom', key: 'max_zoom'},
                {category: 'Stabiliser', key: 'stabiliser'},
                {category: 'FCS', key: 'fcs'},
                {category: 'Thermals', key: 'thermals'},
                {category: 'Rangefinder', key: 'rangefinder'},
                {category: 'APS', key: 'aps'},
            ]
            break;
        case 'turrets':
            Columns = [
                {category: 'Name', key: 'name'},
                {category: 'Tier', key: 'tier'},
                {category: 'Rarity', key: 'rarity'},
                {category: 'Weight', key: 'weight'},
                {category: 'Front Armor', key: 'armor_front'},
                {category: 'Side Armor', key: 'armor_side'},
                {category: 'Rear Armor', key: 'armor_rear'},
                {category: 'Stabiliser', key: 'stabiliser'},
                {category: '↔️ Speed', key: 'h_speed'},
                {category: '↕️ Speed', key: 'v_speed'},
                {category: 'Max Depression', key: 'depression'},
                {category: 'Max Elevation', key: 'elevation'},
                {category: 'Ammo Storage', key: 'ammo_storage'},
                {category: 'Clip', key: 'clip'},
                {category: 'Blowout', key: 'blowout'},
                {category: 'Reload Multi', key: 'reload_multi'},
                {category: 'FCS', key: 'fcs'},
                {category: 'Thermals', key: 'thermals'},
                {category: 'Min Zoom', key: 'min_zoom'},
                {category: 'Max Zoom', key: 'max_zoom'},
                {category: 'Crew Count', key: 'crew'},
                {category: 'APS', key: 'aps'},
                {category: 'Obtain', key: 'obtain'},
                {category: 'Price', key: 'price'},
            ]
            break;
        case 'guns':
            Columns = [
                {category: 'Name', key: 'name'},
                {category: 'Tier', key: 'tier'},
                {category: 'Rarity', key: 'rarity'},
                {category: 'Weight', key: 'weight'},
                {category: 'Accuracy', key: 'accuracy'},
                {category: 'Ammo Volume', key: 'ammo_volume'},
                {category: 'Caliber', key: 'caliber'},
                {category: 'Reload', key: 'reload'},
                {category: 'Obtain', key: 'obtain'},
                {category: 'Price', key: 'price'}
            ]
            break;
        case 'shells':
            Columns = [
                {category: 'AP', key: 'has_ap'},
                {category: 'APHE', key: 'has_aphe'},
                {category: 'APDS', key: 'has_apds'},
                {category: 'APFSDS', key: 'has_apfsds'},
                {category: 'HEAT', key: 'has_heat'},
                {category: 'ATGM', key: 'has_atgm'},
                {category: 'HESH', key: 'has_hesh'},
                {category: 'HE', key: 'has_he'},
                {category: 'Obtain', key: 'obtain'},
                {category: 'Price', key: 'price'}
            ]
            break;
        case 'APHE':
        case 'AP':
        case 'APDS':
        case 'APFSDS':
        case 'HEAT':
        case 'ATGM':
        case 'HESH':
        case 'HE':
            Columns = [
                {category: '0&#176 Penetration', key: 'pen0'},
                {category: '30&#176 Penetration', key: 'pen30'},
                {category: '60&#176 Penetration', key: 'pen60'},
                {category: 'Velocity', key: 'velocity'},
                {category: 'Ricochet Angle', key: 'ricochet_angle'},
                {category: 'Fuse Sensitivity', key: 'fuse_sensitivity'},
                {category: 'Fuse Delay', key: 'fuse_sensitivity'},
                {category: 'Explosive Mass', key: 'filler'},
                {category: 'Range', key: 'range'},
                {category: 'Anti-ERA', key: 'anti_era'},
                {category: 'Tandem', key: 'tandem'},
                {category: 'OTA', key: 'ota'},
                {category: 'PF', key: 'pf'},
                {category: 'Fuse Radius', key: 'fuse_radius'},
                {category: 'Arming Distance', key: 'arming_distance'},
            ]
            break;
        default:
            console.error(`Invalid part type filter: ${filters.type}`)
    }

    //functions go here

    return(
        <table>
            <caption>Caption here</caption>
            <TableHead columns={Columns} />
        <TableBody columns={Columns} tableData={Object.entries(tableData)} />
        </table>
    );
}

export default PartTable;