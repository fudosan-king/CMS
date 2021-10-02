import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'color_yellow': {
                name : translator.t('Yellow'),
                uri: require('./yellow.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.001,
                heightRepeatScale: 0.001,
                mesh : mesh,
                color: '#F9E9D2'
            }   
        };
    },
};