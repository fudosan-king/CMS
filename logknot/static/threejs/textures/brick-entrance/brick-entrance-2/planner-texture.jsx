import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'brick_entrance_2': {
                name : translator.t('Black 2'),
                uri: require('./black-stone.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.007,
                heightRepeatScale: 0.007,
                mesh : mesh,
                // color: '#2E2E2E'
            }   
        };
    },
};