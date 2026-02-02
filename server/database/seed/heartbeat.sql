CREATE OR REPLACE FUNCTION heartbeat()
RETURNS text AS $$
BEGIN
  RETURN 'healthy';
END;
$$ LANGUAGE plpgsql;