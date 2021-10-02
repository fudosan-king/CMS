import Translator from '../../../../src/translator/translator';
import * as Woods from './woods/**/planner-texture.jsx';
import * as Textiles from './textiles/**/planner-texture.jsx';
import * as Metals from './metals/**/planner-texture.jsx';
import * as Stones from './stones/**/planner-texture.jsx';
import * as BrickEntrance from './brick-entrance/**/planner-texture.jsx';
import * as BrickBathroom from './brick-bathroom/**/planner-texture.jsx';
import * as BrickBalcony from './brick-balcony/**/planner-texture.jsx';
import * as Wall from './wall/**/planner-texture.jsx';
import * as Ceilings from './ceilings/**/planner-texture.jsx';
import * as Plastic from './plastic/**/planner-texture.jsx';
import * as Glow from './glow/**/planner-texture.jsx';
import * as Hood from './hood/**/planner-texture.jsx';
import * as Dishwasher from './dishwasher/**/planner-texture.jsx';
import * as Oven from './oven/**/planner-texture.jsx';
import * as Water from './water/**/planner-texture.jsx';
import * as Tap from './tap/**/planner-texture.jsx';
import * as Bathtub from './stone-bathtub/**/planner-texture.jsx';
import * as Glasses from './glasses/**/planner-texture.jsx';
import * as Aluminum from './aluminum/**/planner-texture.jsx';
import * as Paper from './paper/**/planner-texture.jsx';
import * as WoodsArea from './woods-area/**/planner-texture.jsx';
import * as CeilingColor from './ceilings-color/**/planner-texture.jsx';
import * as WoodsKitchen from './woods-kitchen/**/planner-texture.jsx';
import * as StoneKitchen from './stone-kitchen/**/planner-texture.jsx';
import * as PanelKitchen from './panel-kitchen/**/planner-texture.jsx';
import * as ColorArea from './color-area/**/planner-texture.jsx';
import * as Downlight from './downlight/**/planner-texture.jsx';
import * as WoodOakWalnut from './wood-oak-walnut/**/planner-texture.jsx';
import * as SwitchPlate from './entrance-switch-plate/**/planner-texture.jsx';
import * as WcSwitch from './wc-switch/**/planner-texture.jsx';
import * as OutletPlate from './outlet-plate/**/planner-texture.jsx';
import * as Mirror from './mirror/**/planner-texture.jsx';
import * as OutletColor from './outlet-color/**/planner-texture.jsx';
import * as ToiletToTo from './toilet-toto/**/planner-texture.jsx';
import * as FloorCounter from './floor-counter/**/planner-texture.jsx';
import * as WoodKitchen3 from './wood-kitchen3/**/planner-texture.jsx';
import * as Kit from './kit-kitchen/**/planner-texture.jsx';
import * as StoneKitchen3 from './stone-kitchen3/**/planner-texture.jsx';
import * as Chair from './chair/**/planner-texture.jsx';
import * as Window from './window/**/planner-texture.jsx';
import * as WoodOakWalCherry from './wood-oak-wal-cherry/**/planner-texture.jsx';
import * as WhiteSilver from './white-silver/**/planner-texture.jsx';
import * as WoodKitchenFace from './wood-kitchen-face/**/planner-texture.jsx';
import * as DoorWood from './door-storege/**/planner-texture.jsx';
import * as StoneCounter from './stone-counter/**/planner-texture.jsx';
import * as Silver from './silver/**/planner-texture.jsx';
import * as SkirtingWall from './skirting-wall/**/planner-texture.jsx';
import * as BlackStone from './black-stone/**/planner-texture.jsx';
import * as ColorBlock from './color-block/**/planner-texture.jsx';
import * as ColorBlockPaper from './color-block-paper/**/planner-texture.jsx';
import * as SkirtingItems from './skirting-items/**/planner-texture.jsx';
import * as FloorItems from './floor-items/**/planner-texture.jsx';
let translator = new Translator();

export const noneTextures = () => {

    let none = {
        label: translator.t('None'),
        type: 'custom',
        group:'none',
        defaultValue: 'none',
        info: {
            // none: {},
        },
    }
    return none;
};

export const getMultipleTextures = (mesh, type, label = '', hidden = false, defaultValue = '') => {
    let results = [];
    if (type.length > 0 ) {
        type.forEach(element => {
            results.push(getTextures(mesh, element, label, hidden, defaultValue));
        });
    }
    return results;
};

export const getTextures = (mesh, type, label = '', hidden = false, defaultValue = '') =>{

    let defaultItem = defaultValue ? defaultValue : (type + '_default');
    let results = {
        label: translator.t('Wood'),
        type: type,
        group:'wood',
        defaultValue: 'wood_default',
        info: {},
        hidden: hidden,
    };
    let currentTextures = {};
    switch(type) {
        case 'textile': 
            currentTextures = Textiles;
            results.label = translator.t('Textile');
            results.group = 'textile';
            results.defaultValue = defaultItem
            break;
        case 'metal': 
            currentTextures = Metals;
            results.label = translator.t('Metal');
            results.group = 'metal';
            results.defaultValue = defaultItem
            break;
        case 'stone': 
            currentTextures = Stones;
            results.label = translator.t('Stone');
            results.group = 'stone';
            results.defaultValue = defaultItem;
            break;
        case 'brick_entrance': 
            currentTextures = BrickEntrance;
            results.label = 'BrickEntrance';
            results.group = 'brick-entrance';
            results.defaultValue = defaultItem;
            break;
        case 'brick_bathroom': 
            currentTextures = BrickBathroom;
            results.label = 'BrickBathroom';
            results.group = 'brick-bathroom';
            results.defaultValue = defaultItem;
            break;
        case 'brick_balcony': 
            currentTextures = BrickBalcony;
            results.label = 'BrickBalcony';
            results.group = 'brick-balcony';
            results.defaultValue = defaultItem;
            break;
        case 'wall': 
            currentTextures = Wall;
            results.label = translator.t('Wall');
            results.group = 'wall';
            results.defaultValue = defaultItem;
            break;
        case 'ceilings': 
            currentTextures = Ceilings;
            results.label = translator.t('Ceilings');
            results.group = 'ceilings';
            results.defaultValue = '';
            break;
        case 'plastic': 
            currentTextures = Plastic;
            results.label = translator.t('Plastic');
            results.group = 'plastic';
            results.defaultValue = defaultItem;
            break;
        case 'glow': 
            currentTextures = Glow;
            results.label = translator.t('Glow');
            results.group = 'glow';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'dishwasher': 
            currentTextures = Dishwasher;
            results.label = translator.t('Dishwasher');
            results.group = 'dishwasher';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'hood': 
            currentTextures = Hood;
            results.label = translator.t('Hood');
            results.group = 'hood';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'oven': 
            currentTextures = Oven;
            results.label = translator.t('Oven');
            results.group = 'oven';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'water': 
            currentTextures = Water;
            results.label = translator.t('Water');
            results.group = 'water';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'tap': 
            currentTextures = Tap;
            results.label = translator.t('Tap');
            results.group = 'tap';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'bathtub': 
            currentTextures = Bathtub;
            results.label = translator.t('Bathtub');
            results.group = 'bathtub';
            results.defaultValue = defaultItem;
            break;
        case 'glasses': 
            currentTextures = Glasses;
            results.label = translator.t('Glasses');
            results.group = 'glasses';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'aluminum': 
            currentTextures = Aluminum;
            results.label = translator.t('Aluminum');
            results.group = 'aluminum';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'paper': 
            currentTextures = Paper;
            results.label = translator.t('Paper');
            results.group = 'paper';
            results.defaultValue = defaultItem;
            results.hidden = true;
            break;
        case 'woods_area': 
            currentTextures = WoodsArea;
            results.label = translator.t('Wood');
            results.group = 'woods-area';
            results.defaultValue = defaultItem;
            break;
        case 'ceilings_color': 
            currentTextures = CeilingColor;
            results.label = translator.t('Color');
            results.group = 'ceilings-color';
            results.defaultValue = defaultItem;
            break;
        case 'wood-kitchen':
            currentTextures = WoodsKitchen;
            results.label = translator.t('Kitchen wood');
            results.group = 'wood-kitchen';
            results.defaultValue = defaultItem;
            results.hidden = false;
            break;
        case 'stone-kitchen':
            currentTextures = StoneKitchen;
            results.label = translator.t('Kitchen stone');
            results.group = 'stone-kitchen';
            results.defaultValue = defaultItem;
            break;
        case 'panel-kitchen':
            currentTextures = PanelKitchen;
            results.label = translator.t('Kitchen panel');
            results.group = 'panel-kitchen';
            results.defaultValue = defaultItem;
            break;
        case 'color-area':
            currentTextures = ColorArea;
            results.label = translator.t('Color');
            results.group = 'color-area';
            results.defaultValue = defaultItem;
            break;
        case 'downlight':
            currentTextures = Downlight;
            results.label = translator.t('Downlight');
            results.group = 'downlight';
            results.defaultValue = defaultItem;
            break;
        case 'wood-oak-walnut':
            currentTextures = WoodOakWalnut;
            results.label = translator.t('Wood Oak Walnut');
            results.group = 'wood-oak-walnut';
            results.defaultValue = defaultItem;
            break;
        case 'switch-plate':
            currentTextures = SwitchPlate;
            results.label = translator.t('Switch plate');
            results.group = 'switch-plate';
            results.defaultValue = defaultItem;
            break;
        case 'wc-switch':
            currentTextures = WcSwitch;
            results.label = translator.t('Wc switch');
            results.group = 'wc-switch';
            results.defaultValue = defaultItem;
            break;
        case 'outlet-plate':
            currentTextures = OutletPlate;
            results.label = translator.t('Outlet plate');
            results.group = 'outlet-plate';
            results.defaultValue = defaultItem;
            break;
        case 'mirror':
            currentTextures = Mirror;
            results.label = translator.t('Mirror');
            results.group = 'mirror';
            results.defaultValue = defaultItem;
            break;
        case 'outlet-color':
            currentTextures = OutletColor;
            results.label = translator.t('Color');
            results.group = 'outlet-color';
            results.defaultValue = defaultItem;
            break;
        case 'toilet-toto':
            currentTextures = ToiletToTo;
            results.label = translator.t('Color');
            results.group = 'outlet-color';
            results.defaultValue = defaultItem;
            break;
        case 'floor-counter':
            currentTextures = FloorCounter;
            results.label = translator.t('Floor Counter');
            results.group = 'floor-counter';
            results.defaultValue = defaultItem;
            break;
        case 'wood-kitchen3':
            currentTextures = WoodKitchen3;
            results.label = translator.t('Wood Kitchen 3');
            results.group = 'wood-kitchen3';
            results.defaultValue = defaultItem;
            break;
        case 'kit':
            currentTextures = Kit;
            results.label = translator.t('Kit');
            results.group = 'kit';
            results.defaultValue = defaultItem;
            break;
        case 'stone-kitchen3':
            currentTextures = StoneKitchen3;
            results.label = translator.t('Stone');
            results.group = 'stone-kitchen3';
            results.defaultValue = defaultItem;
            break;
        case 'chair':
            currentTextures = Chair;
            results.label = translator.t('Cushion');
            results.group = 'chair';
            results.defaultValue = defaultItem;
            break;
        case 'window':
            currentTextures = Window;
            results.label = translator.t('Color');
            results.group = 'window';
            results.defaultValue = defaultItem;
            break;
        case 'wood-oak-wal-cherry':
            currentTextures = WoodOakWalCherry;
            results.label = translator.t('Wood');
            results.group = 'wood-oak-wal-cherry';
            results.defaultValue = defaultItem;
            break;
        case 'white-silver':
            currentTextures = WhiteSilver;
            results.label = translator.t('Metal');
            results.group = 'white-silver';
            results.defaultValue = defaultItem;
            break;
        case 'wood-kitchen-face':
            currentTextures = WoodKitchenFace;
            results.label = translator.t('Wood');
            results.group = 'wood-kitchen-face';
            results.defaultValue = defaultItem;
            break;
        case 'door-wood':
            currentTextures = DoorWood;
            results.label = translator.t('Wood');
            results.group = 'door-wood';
            results.defaultValue = defaultItem;
            break;
        case 'stone-counter':
            currentTextures = StoneCounter;
            results.label = translator.t('Stone');
            results.group = 'stone-counter';
            results.defaultValue = defaultItem;
            break;
        case 'silver':
            currentTextures = Silver;
            results.label = translator.t('Silver');
            results.group = 'silver';
            results.defaultValue = defaultItem;
            break;
        case 'skirting':
            currentTextures = SkirtingWall;
            results.label = translator.t('Skirting Wall');
            results.group = 'skirting';
            results.defaultValue = defaultItem;
            break;
        case 'black-stone':
            currentTextures = BlackStone;
            results.label = translator.t('Black');
            results.group = 'black-stone';
            results.defaultValue = defaultItem;
            break;
        case 'color-block':
            currentTextures = ColorBlock;
            results.label = translator.t('Color');
            results.group = 'color-block';
            results.defaultValue = defaultItem;
            break;
        case 'color-block-paper':
            currentTextures = ColorBlockPaper;
            results.label = translator.t('Color');
            results.group = 'color-block-paper';
            results.defaultValue = defaultItem;
            break;
        case 'skirting-items':
            currentTextures = SkirtingItems;
            results.label = translator.t('Color');
            results.group = 'skirting-items';
            results.defaultValue = defaultItem;
            break;
        case 'floor-items':
            currentTextures = FloorItems;
            results.label = translator.t('Floor');
            results.group = 'floor-items';
            results.defaultValue = defaultItem;
            break;
        case 'wood': 
        default: 
            currentTextures = Woods;
            break;
    }

    if (label !== '') {
        results.label = label;
    }
    for( let i in currentTextures ) {
        let properties = currentTextures[i].textureProperties(mesh);
        let key = Object.keys(properties)[0];
        results.info[key] = properties[key];
    }

   return results;
};

export const getTextureProperties = (properties, element, mode = '3d') => {
    let results = [];   
    for (let key in properties) {
        if (properties[key].type == 'textures') {
            let currentTextures = null;
            try{
                if (element.properties.getIn([key]).size > 0) {
                    currentTextures = properties[key].values;
                    
                    element.properties.getIn([key]).forEach((item, index) => {
                        if (mode === '2d') {
                            results[key] = currentTextures[index].info[item].color;
                        } else {
                            results.push(currentTextures[index].info[item]);
                        }
                    });
                }
            } catch(error) {
                console.log(error.message);
            }
        }
    }
    return results;
};