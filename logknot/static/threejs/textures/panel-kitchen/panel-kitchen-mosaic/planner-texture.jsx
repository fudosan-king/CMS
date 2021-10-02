import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'panel_kitchen_mosaic': {
                name : translator.t('Mosaic'),
                uri: require('./mosaic-tile.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#DAD7D0'
            }   
        };
    },
};