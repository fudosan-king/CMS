import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_tile_aqua': {
                name : translator.t('Cafe tile aqua'),
                uri: require('./cafe-tile-aqua.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E0F8E6'
            }   
        };
    },
};