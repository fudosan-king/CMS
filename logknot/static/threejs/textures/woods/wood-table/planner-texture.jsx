import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_table': {
                name : translator.t('Wood table'),
                uri: require('./wood_90.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#c38653'
            }   
        };
    },
};