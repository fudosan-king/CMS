import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_door2': {
                name : translator.t('Wood') + ' 2',
                uri: require('./wood_2.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#caa163'
            }   
        };
    },
};