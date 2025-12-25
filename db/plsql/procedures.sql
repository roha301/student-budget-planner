-- Sample PL/SQL stored procedure to get monthly spend by category
CREATE OR REPLACE PROCEDURE get_monthly_spend(
  p_user_id IN NUMBER,
  p_year IN NUMBER,
  p_month IN NUMBER,
  p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
  OPEN p_cursor FOR
    SELECT c.name as category, SUM(e.amount) as total
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    WHERE e.user_id = p_user_id
      AND EXTRACT(YEAR FROM e.exp_date) = p_year
      AND EXTRACT(MONTH FROM e.exp_date) = p_month
    GROUP BY c.name;
END;
/

-- Example procedure for budget check
CREATE OR REPLACE PROCEDURE check_budget(
  p_user_id IN NUMBER,
  p_budget_id IN NUMBER,
  p_status OUT VARCHAR2
) AS
  v_spent NUMBER;
  v_limit NUMBER;
BEGIN
  SELECT SUM(amount) INTO v_spent FROM expenses WHERE user_id = p_user_id AND category_id IN (SELECT id FROM categories WHERE user_id = p_user_id);
  SELECT amount INTO v_limit FROM budgets WHERE id = p_budget_id;
  IF v_spent > v_limit THEN
    p_status := 'OVER';
  ELSE
    p_status := 'OK';
  END IF;
END;
/