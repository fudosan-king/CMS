import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
import {getBase64Code} from './base64'
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_blonde': {
                name : translator.t('Blonde'),
                uri: require('./wood_blonde.jpg'),
                base64: getBase64Code(),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F6E3CE'
            }   
        };
    },
};