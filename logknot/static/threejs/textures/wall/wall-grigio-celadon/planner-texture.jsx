import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_grigio_celadon': {
                name : translator.t('Grigio celadon'),
                uri: require('./grigio_celadon.jpg'),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                normalScaleX: 0.01,
                normalScaleY: 0.01,
                mesh : mesh,
                color:'#AEBCBB' 
            }   
        };
    },
};