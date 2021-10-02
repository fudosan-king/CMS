import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_paper_4': {
                name : translator.t('Paper 4'),
                uri: require('./paper4.jpg'),
                lengthRepeatScale: 0.005,
                heightRepeatScale: 0.005,
                // normalScaleX: 0.01,
                // normalScaleY: 0.01,
                mesh : mesh,
                color:'#FFFFFF' 
            }   
        };
    },
};