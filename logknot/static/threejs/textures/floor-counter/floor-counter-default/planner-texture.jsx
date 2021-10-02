import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'floor_counter_default': {
                name : translator.t('Default'),
                uri: require('./white.jpg'),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                normalScaleX: 0.01,
                normalScaleY: 0.01,
                mesh : mesh,
                color:'#FFFFFF' 
            }   
        };
    },
};