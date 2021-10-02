import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_botechino_beige': {
                name : translator.t('Botechino beige'),
                uri: require('./botechino_beige.jpg'),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                normalScaleX: 0.01,
                normalScaleY: 0.01,
                mesh : mesh,
                color:'#F4DAB5' 
            }   
        };
    },
};