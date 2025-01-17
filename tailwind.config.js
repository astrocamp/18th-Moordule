/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["**/templates/**/*.{html,js}"],
	theme: {
		extend: {
			spacing: {
				'21': '5.25rem',
				'22': '5.5rem',
				'23': '5.75rem',
				'24': '6.0rem',
			},
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
