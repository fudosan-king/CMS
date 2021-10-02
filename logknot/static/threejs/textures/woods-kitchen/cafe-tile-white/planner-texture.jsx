import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_tile_white': {
                name : translator.t('Cafe tile white'),
                uri: require('./cafe-tile-white.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#D4DFCF'
            }   
        };
    },
};