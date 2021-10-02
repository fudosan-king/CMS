import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'skirting_default': {
                name : translator.t('Default'),
                uri: require('./lentuong.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 0.001,
                normalScaleX: 0.01,
                normalScaleY: 0.01,
                mesh : mesh,
                color:'#61210B' 
            }   
        };
    },
};