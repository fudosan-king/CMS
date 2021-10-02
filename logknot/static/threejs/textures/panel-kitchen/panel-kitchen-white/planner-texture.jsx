import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'panel_kitchen_white': {
                name : translator.t('White cloud'),
                uri: require('./white-cloud.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F9F9F7'
            }   
        };
    },
};