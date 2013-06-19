
var Quiz = Backbone.Model.extend({
	url : function() {
		return '/api/quiz' + (this.get('id')? ('/'+this.get('id')) : '');	
	} 
});

var Question = Backbone.Model.extend({

	initialize : function(opts) {
		this.quiz = opts.quiz;
	},

	url : function() {
		return this.quiz.url() + '/questions' + (this.get('id')? ('/'+this.get('id')) : '');
	}
});


var InitQuizView = NiceView.extend({

	el : '#quiz-body',

	events : _.extend({}, NiceView.prototype.evs, {
		'click #init-quiz' : 'initQuiz'
	}),

	initialize : function() {
		loadTemplate('init-quiz-template', '/static/templates/quiz/init.html');
		this.template = _.template($('#init-quiz-template').html());
		this.render();
	},


	render : function(errors) {
		var formVals = this.pushform();
		this.$el.html(this.template({
			errors : errors? errors.errors : errors
		}));
		this.popform(formVals);
	},

	initQuiz : function() {
		var that = this;
		var data = this.$el.find('#init-form').serializeObject();
		var quiz = new Quiz(data);
		quiz.sync('create', quiz, {wait : true,
			success : function(model, resp, opts) {
				var qv = new QuestionView({
					quiz : quiz.set(model)
				});
			},
			error : function(resp) {
				errors = JSON.parse(resp.responseText);
				that.render(errors);
			}

		});
	}
});

var QuestionView = NiceView.extend({

	el : '#quiz-body',

	events : _.extend({}, NiceView.prototype.evs, {
		'click .answer-now' : 'answerNow',
		'click .answer-later' : 'answerLater',
		
	}),

	initialize : function(opts) {
		this.quiz = opts.quiz;
		loadTemplate('question-template', '/static/templates/quiz/question.html');
		this.template = _.template($('#question-template').html());
		this.getQuestion();
		_.bindAll(this, 'keyAnswer');
		$(document).keyup(this.keyAnswer);
	},

	getQuestion : function() {
		var that = this;
		this.question = new Question({quiz : this.quiz});
		this.question.fetch({
			wait : true,
			success : function(model, resp, opts) {
				that.question = model;
				that.render();
			},
			error : function() {
			}
		});
	},

	keyAnswer : function(e) {
		e.keyCode === 76 && this.answerLater();
		e.keyCode === 78 && this.answerNow();
	},

	answerNow : function() {
		this.answer(true);
	},

	answerLater : function() {
		this.answer(false);
	},

	answer : function(now) {
		var that = this;
		this.question.set('choice', now);
		this.question.set('session', this.quiz.get('session'));
		this.question.sync('update', this.question, {
			wait : true, 
			success : function() {
				if(that.question.get('order') >= 10) {
					window.location = '/result/'+that.quiz.get('id')
				} else {
					that.getQuestion();
				}
			}
		});
	},

	render : function(errors) {
		var that = this;
		this.$el.html(this.template({
			question : that.question.toJSON()
		}));
	}



});







$(document).ready(function() {
	app.views.quiz = new InitQuizView();
});