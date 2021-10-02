import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64';
export default {
    textureProperties: function (mesh) {
        return { 
            'brick_bathroom_2': {
                name : translator.t('Granite light'),
                uri: require('./granite_light.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                mesh : mesh,
                color: '#F1DAA8'
            }   
        };
    },
};