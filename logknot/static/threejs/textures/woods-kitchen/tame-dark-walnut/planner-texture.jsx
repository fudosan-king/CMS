import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'tame_darkWalnut': {
                name : translator.t('Dark walnut'),
                uri: require('./dark-walnut.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#765949'
            }   
        };
    },
};