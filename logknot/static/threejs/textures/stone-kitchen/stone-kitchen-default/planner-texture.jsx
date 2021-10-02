import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'stone_default': {
                name : translator.t('White cloud'),
                uri: require('./white-cloud.jpg'),
                lengthRepeatScale: 0.1,
                heightRepeatScale: 0.1,
                mesh : mesh,
                color: '#F9F9F7'
            }   
        };
    },
};