import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_amugis': {
                name : translator.t('Amugis'),
                uri: require('./4.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                mesh : mesh,
                color: '#B45F04'
            }   
        };
    },
};