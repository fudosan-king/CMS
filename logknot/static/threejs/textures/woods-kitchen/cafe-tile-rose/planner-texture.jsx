import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_tile_rose': {
                name : translator.t('Cafe tile rose'),
                uri: require('./cafe-tile-rose.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E3D9D7'
            }   
        };
    },
};