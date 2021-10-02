import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'brick_bathroom_4': {
                name : translator.t('Grey'),
                uri: require('./grey.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.02,
                heightRepeatScale: 0.02,
                mesh : mesh,
                color: '#FAFAFA'
            }   
        };
    },
};