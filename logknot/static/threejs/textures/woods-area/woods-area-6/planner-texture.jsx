import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_area_6': {
                name : translator.t('Walnut 1'),
                uri: require('./7.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.003,
                heightRepeatScale: 0.003,
                mesh : mesh,
                // color: '#72534A'
            }   
        };
    },
};