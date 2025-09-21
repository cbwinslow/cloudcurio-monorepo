import { describe, it, expect } from '@jest/globals';
import { validateRequest, reviewJobSchema, claimJobSchema, completeJobSchema } from '../lib/validation';

describe('Validation utilities', () => {
  describe('reviewJobSchema', () => {
    it('should validate correct review job data', () => {
      const data = {
        repoUrl: 'https://github.com/user/repo',
        klass: 'quick'
      };
      
      const result = validateRequest(reviewJobSchema, data);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(data);
      }
    });

    it('should reject invalid repo URL', () => {
      const data = {
        repoUrl: 'not-a-url',
        klass: 'quick'
      };
      
      const result = validateRequest(reviewJobSchema, data);
      expect(result.success).toBe(false);
    });

    it('should provide default klass when not provided', () => {
      const data = {
        repoUrl: 'https://github.com/user/repo'
      };
      
      const result = validateRequest(reviewJobSchema, data);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.klass).toBe('quick');
      }
    });
  });

  describe('claimJobSchema', () => {
    it('should validate correct claim job data', () => {
      const data = {
        gpu: 'rtx3060',
        classes: ['quick', 'heavy']
      };
      
      const result = validateRequest(claimJobSchema, data);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(data);
      }
    });

    it('should provide default classes when not provided', () => {
      const data = {
        gpu: 'rtx3060'
      };
      
      const result = validateRequest(claimJobSchema, data);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.classes).toEqual([]);
      }
    });
  });

  describe('completeJobSchema', () => {
    it('should validate correct complete job data', () => {
      const data = {
        status: 'done',
        content: '<html>test</html>',
        error: null,
        gpu: 'rtx3060'
      };
      
      const result = validateRequest(completeJobSchema, data);
      expect(result.success).toBe(true);
    });
  });
});