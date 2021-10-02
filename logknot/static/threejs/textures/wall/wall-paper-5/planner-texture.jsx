import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_paper_5': {
                name : translator.t('Paper new 1'),
                uri: require('./paper5.jpg'),
                lengthRepeatScale: 0.003,
                heightRepeatScale: 0.003,
                // normalScaleX: 0.01,
                // normalScaleY: 0.01,
                mesh : mesh,
                // color:'#FFFFFF' 
            }   
        };
    },
};