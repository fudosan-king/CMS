import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_paper_4': {
                name : translator.t('Paper new'),
                uri: require('./paper4.jpg'),
                lengthRepeatScale: 0.5,
                heightRepeatScale: 0.5,
                // normalScaleX: 0.01,
                // normalScaleY: 0.01,
                mesh : mesh,
                color:'#FFFFFF' 
            }   
        };
    },
};