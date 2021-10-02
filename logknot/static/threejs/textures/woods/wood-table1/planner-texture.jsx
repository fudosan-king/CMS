import Translator from '../../../../../../src/translator/translator';
import {getBase64Code} from './base64';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_table1': {
                name : translator.t('Wood table 1'),
                uri: require('./wood2_90.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#cda778'
            }   
        };
    },
};