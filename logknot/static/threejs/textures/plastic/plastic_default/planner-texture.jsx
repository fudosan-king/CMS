import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'plastic_default': {
                name : translator.t('White'),
                uri: require('./plastic.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#EBEAEA'
            }   
        };
    },
};