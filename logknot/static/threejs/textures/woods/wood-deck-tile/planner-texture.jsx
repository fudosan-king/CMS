import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_deck_tile': {
                name : translator.t('Wood deck tile'),
                uri: require('./wood_deck.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                mesh : mesh,
                color: '#F5D0A9'
            }   
        };
    },
};