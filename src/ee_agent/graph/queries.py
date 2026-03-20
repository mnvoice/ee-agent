"""Cypher query constants for Neo4j operations."""


class CypherQueries:
    # Schema initialization - constraints
    CREATE_PROBLEM_CONSTRAINT = """
        CREATE CONSTRAINT problem_id IF NOT EXISTS
        FOR (p:Problem) REQUIRE p.id IS UNIQUE
    """
    CREATE_CONCEPT_CONSTRAINT = """
        CREATE CONSTRAINT concept_name IF NOT EXISTS
        FOR (c:Concept) REQUIRE c.name IS UNIQUE
    """
    CREATE_FORMULA_CONSTRAINT = """
        CREATE CONSTRAINT formula_id IF NOT EXISTS
        FOR (f:Formula) REQUIRE f.id IS UNIQUE
    """
    CREATE_REGULATION_CONSTRAINT = """
        CREATE CONSTRAINT regulation_article IF NOT EXISTS
        FOR (r:Regulation) REQUIRE r.article IS UNIQUE
    """
    CREATE_SUBJECT_CONSTRAINT = """
        CREATE CONSTRAINT subject_name IF NOT EXISTS
        FOR (s:Subject) REQUIRE s.name IS UNIQUE
    """

    # Fulltext indexes for Korean text search
    CREATE_PROBLEM_FULLTEXT = """
        CREATE FULLTEXT INDEX problem_text_idx IF NOT EXISTS
        FOR (p:Problem) ON EACH [p.stem, p.explanation]
    """
    CREATE_CONCEPT_FULLTEXT = """
        CREATE FULLTEXT INDEX concept_text_idx IF NOT EXISTS
        FOR (c:Concept) ON EACH [c.name, c.definition]
    """

    # UPSERT queries
    MERGE_SUBJECT = """
        MERGE (s:Subject {name: $name})
        ON CREATE SET s.created_at = datetime()
        RETURN s
    """
    MERGE_PROBLEM = """
        MERGE (p:Problem {id: $id})
        ON CREATE SET
            p.year = $year,
            p.exam_session = $exam_session,
            p.question_number = $question_number,
            p.subject = $subject,
            p.question_type = $question_type,
            p.difficulty = $difficulty,
            p.stem = $stem,
            p.correct_answer = $correct_answer,
            p.explanation = $explanation,
            p.tags = $tags,
            p.has_image = $has_image,
            p.created_at = datetime()
        ON MATCH SET
            p.updated_at = datetime()
        RETURN p
    """
    MERGE_CONCEPT = """
        MERGE (c:Concept {name: $name})
        ON CREATE SET
            c.id = $id,
            c.definition = $definition,
            c.subject = $subject,
            c.korean_terms = $korean_terms,
            c.created_at = datetime()
        RETURN c
    """
    MERGE_FORMULA = """
        MERGE (f:Formula {id: $id})
        ON CREATE SET
            f.name = $name,
            f.latex = $latex,
            f.description = $description,
            f.applicable_subjects = $applicable_subjects,
            f.created_at = datetime()
        RETURN f
    """
    MERGE_REGULATION = """
        MERGE (r:Regulation {article: $article})
        ON CREATE SET
            r.id = $id,
            r.content = $content,
            r.keywords = $keywords,
            r.created_at = datetime()
        RETURN r
    """

    # Relationship queries
    LINK_PROBLEM_SUBJECT = """
        MATCH (p:Problem {id: $problem_id})
        MATCH (s:Subject {name: $subject_name})
        MERGE (p)-[:BELONGS_TO]->(s)
    """
    LINK_PROBLEM_CONCEPT = """
        MATCH (p:Problem {id: $problem_id})
        MATCH (c:Concept {name: $concept_name})
        MERGE (p)-[:REQUIRES]->(c)
    """
    LINK_PROBLEM_FORMULA = """
        MATCH (p:Problem {id: $problem_id})
        MATCH (f:Formula {id: $formula_id})
        MERGE (p)-[:APPLIES]->(f)
    """
    LINK_PROBLEM_REGULATION = """
        MATCH (p:Problem {id: $problem_id})
        MATCH (r:Regulation {article: $article})
        MERGE (p)-[:REFERENCES]->(r)
    """
    LINK_CONCEPT_DEPENDS = """
        MATCH (c1:Concept {name: $concept_a})
        MATCH (c2:Concept {name: $concept_b})
        MERGE (c1)-[:DEPENDS_ON]->(c2)
    """

    # Query queries
    GET_PROBLEM_BY_ID = """
        MATCH (p:Problem {id: $id})
        OPTIONAL MATCH (p)-[:REQUIRES]->(c:Concept)
        OPTIONAL MATCH (p)-[:APPLIES]->(f:Formula)
        OPTIONAL MATCH (p)-[:BELONGS_TO]->(s:Subject)
        RETURN p, collect(DISTINCT c.name) AS concepts,
               collect(DISTINCT f.name) AS formulas, s.name AS subject
    """
    GET_CONCEPTS_FOR_SUBJECT = """
        MATCH (p:Problem)-[:BELONGS_TO]->(s:Subject {name: $subject})
        MATCH (p)-[:REQUIRES]->(c:Concept)
        RETURN c.name AS concept, count(p) AS problem_count
        ORDER BY problem_count DESC
    """
    GET_PROBLEM_CONCEPT_CHAIN = """
        MATCH (p:Problem {difficulty: $difficulty})-[:REQUIRES*1..3]->(c:Concept)
        RETURN p.id AS problem_id, collect(DISTINCT c.name) AS concept_chain
        LIMIT $limit
    """
    GET_SUBJECT_STATS = """
        MATCH (p:Problem)-[:BELONGS_TO]->(s:Subject)
        RETURN s.name AS subject, count(p) AS count
        ORDER BY count DESC
    """
    FULLTEXT_SEARCH_PROBLEMS = """
        CALL db.index.fulltext.queryNodes('problem_text_idx', $query)
        YIELD node, score
        RETURN node, score
        ORDER BY score DESC
        LIMIT $limit
    """
