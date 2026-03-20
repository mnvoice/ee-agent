from rdflib import Namespace, URIRef

EE = Namespace("http://ee-agent.kr/ontology#")


class EEClass:
    PROBLEM = EE.Problem
    CONCEPT = EE.Concept
    FORMULA = EE.Formula
    REGULATION = EE.Regulation
    SUBJECT = EE.Subject
    DIAGRAM = EE.DiagramTopology


class EEProperty:
    REQUIRES = EE.requires
    APPLIES = EE.applies
    REFERENCES = EE.references
    BELONGS_TO = EE.belongsTo
    DEPENDS_ON = EE.dependsOn
    HAS_TOPOLOGY = EE.hasTopology
    QUESTION_TEXT = EE.questionText
    CORRECT_ANS = EE.correctAnswer
    YEAR = EE.year
    LATEX_EXPR = EE.latexExpression
    ARTICLE_NUM = EE.articleNumber
    DIFFICULTY = EE.difficultyScore
