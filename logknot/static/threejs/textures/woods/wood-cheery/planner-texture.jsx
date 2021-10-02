import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_cheery': {
                name : translator.t('Cheery'),
                uri: require('./7.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                mesh : mesh,
                color: '#F6D8CE'
            }   
        };
    },
};