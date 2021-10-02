import Translator from '../../../../../../src/translator/translator';
import {getBase64Code} from './base64'
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_default': {
                name : translator.t('Default'),
                uri: require('./wood_default.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#7f5c48'
            }   
        };
    },
};