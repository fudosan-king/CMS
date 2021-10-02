import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_area_10': {
                name : translator.t('Walnut new'),
                uri: require('./wood.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.0035,
                heightRepeatScale: 0.0035,
                mesh : mesh,
                color: '#FCEBE6'
            }   
        };
    },
};