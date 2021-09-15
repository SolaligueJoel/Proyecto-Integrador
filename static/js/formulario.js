const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const name = document.getElementById('name')

const formulario2 = document.getElementById('formulario2')

const expresiones = {
	user: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	name: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	password: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/, //Mínimo ocho caracteres, al menos una letra y un número.
	email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/
}



const campos = {
	user_name: false,
	email: false,
	password: false
}



const validarFormulario = (e)=>{
	switch (e.target.name){
		case "user_name":
			validarCampo(expresiones.user, e.target,'usuario');
		break;
		
		case "email":
			validarCampo(expresiones.email,e.target,'correo')
			break;
			
		case "password":
			validarCampo(expresiones.password,e.target,'password')
			validarPassword2()
		break;
		case "password2":
			validarPassword2()
		break;
	}
	}


const validarCampo = (expresion, input, campo)=>{
	if(expresion.test(input.value)){
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo')
		campos[campo] = true;

	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;

	}
}


const validarPassword2 = ()=>{
	const inputPssword1 = document.getElementById('password');
	const inputPssword2 = document.getElementById('password2');

	if(inputPssword1.value !== inputPssword2.value){
		document.getElementById(`grupo__password2`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__password2`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__password2 i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__password2 i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__password2 .formulario__input-error`).classList.add('formulario__input-error-activo')
		campos['password'] = false
	} else{
		document.getElementById(`grupo__password2`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__password2`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__password2 i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__password2 i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__password2 .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos['password'] = true;

	}
}

inputs.forEach((input)=>{
	input.addEventListener('keyup',validarFormulario)
	input.addEventListener('blur',validarFormulario)
})


formulario.addEventListener('submit',(e)=>{
	const terminos = document.getElementById('terminos');
	if (!(campos.user_name || campos.email || campos.password && terminos.checked)){
		e.preventDefault()
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo')
		setTimeout(()=>{
			document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo')
		},4000);
	} 
});

