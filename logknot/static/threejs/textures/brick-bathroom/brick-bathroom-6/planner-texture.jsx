import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'brick_bathroom_6': {
                name : translator.t('Grey new'),
                uri: require('./grey.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.014,
                heightRepeatScale: 0.006,
                mesh : mesh,
                // color: '#FAFAFA'
            }   
        };
    },
};