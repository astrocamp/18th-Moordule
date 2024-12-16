/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["**/templates/**/*.{html,js}"],
	theme: {
		extend: {
			colors: {
				moordule: {
					pink: "#F78888",
					yellow: "#F6D246",
					gray: "#ECECEC",
					"light-blue": "#90CCF4",
					"deep-blue": "#5DA2D5",
				},
			},
		},
	},
	plugins: [],
};
