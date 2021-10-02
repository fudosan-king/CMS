import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_area_8': {
                name : translator.t('Walnut 8'),
                uri: require('./8.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.008,
                heightRepeatScale: 0.008,
                mesh : mesh,
                // color: '#72534A'
            }   
        };
    },
};