import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_kumiishi_beige': {
                name : translator.t('Kumiishi beig'),
                uri: require('./kumiishi_beige.jpg'),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                normalScaleX: 0.01,
                normalScaleY: 0.01,
                mesh : mesh,
                color:'#FAECD7' 
            }   
        };
    },
};