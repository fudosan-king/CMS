import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_pullable_blue': {
                name : translator.t('Pullable blue'),
                uri: require('./pullable-blue.jpg'),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                normalScaleX: 0.01,
                normalScaleY: 0.01,
                mesh : mesh,
                color:'#043F7A' 
            }   
        };
    },
};