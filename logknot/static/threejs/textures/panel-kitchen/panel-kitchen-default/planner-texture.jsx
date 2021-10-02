import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'panel_kitchen_default': {
                name : translator.t('Greige'),
                uri: require('./greige-wood.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#C7C8C3'
            }   
        };
    },
};